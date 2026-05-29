"""
Agent Registry - 统一Agent注册表
管理所有可用Agent的注册、发现和调用
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AgentDefinition:
    """Agent定义"""
    name: str
    role: str
    description: str
    capabilities: List[str]
    system_prompt: str = ""
    handoff_template: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentRegistry:
    """
    Agent注册表
    
    统一管理所有Agent的定义和发现
    """
    
    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = Path(agents_dir)
        self._agents: Dict[str, AgentDefinition] = {}
        self._load_agents()
    
    def _load_agents(self):
        """从agents目录加载所有Agent定义"""
        if not self.agents_dir.exists():
            return
        
        for agent_file in self.agents_dir.glob("*_agent.md"):
            agent_name = agent_file.stem.replace("_agent", "")
            self._agents[agent_name] = self._parse_agent_file(agent_file)
    
    def _parse_agent_file(self, file_path: Path) -> AgentDefinition:
        """解析Agent定义文件"""
        content = file_path.read_text(encoding="utf-8")
        
        # 提取基本信息
        name = self._extract_section(content, "## Agent", file_path.stem)
        role = self._extract_section(content, "## Role", "")
        description = self._extract_section(content, "## Description", "")
        
        # 提取能力列表
        capabilities = []
        cap_match = content.find("## Capabilities")
        if cap_match != -1:
            cap_section = content[cap_match:].split("##")[0]
            capabilities = [line.strip("- ").strip() 
                          for line in cap_section.split("\n") 
                          if line.strip().startswith("-")]
        
        return AgentDefinition(
            name=name,
            role=role,
            description=description,
            capabilities=capabilities,
            system_prompt=content
        )
    
    def _extract_section(self, content: str, section: str, default: str) -> str:
        """提取markdown章节内容"""
        import re
        pattern = rf"{section}\s*\n([^#]+)"
        match = re.search(pattern, content)
        return match.group(1).strip() if match else default
    
    def get(self, name: str) -> Optional[AgentDefinition]:
        """获取指定Agent"""
        return self._agents.get(name)
    
    def list_agents(self) -> List[str]:
        """列出所有可用Agent"""
        return list(self._agents.keys())
    
    def find_by_capability(self, capability: str) -> List[AgentDefinition]:
        """按能力查找Agent"""
        return [agent for agent in self._agents.values() 
                if capability in agent.capabilities]
    
    def get_system_prompt(self, name: str) -> str:
        """获取Agent的系统提示词"""
        agent = self.get(name)
        return agent.system_prompt if agent else ""
    
    def register(self, name: str, definition: AgentDefinition):
        """注册新Agent"""
        self._agents[name] = definition
    
    def to_dict(self) -> Dict:
        """导出为字典"""
        return {
            name: {
                "name": agent.name,
                "role": agent.role,
                "description": agent.description,
                "capabilities": agent.capabilities
            }
            for name, agent in self._agents.items()
        }


# 全局注册表实例
_registry = None


def get_registry() -> AgentRegistry:
    """获取全局Agent注册表实例"""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry
