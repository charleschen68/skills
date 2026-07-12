# gowork/__init__.py
"""User skills directory.

Import skills here for automatic registration.
"""

from gowork.blog_summarize import BlogSummarizeSkill
from gowork.create_skill_demo import CreateSkillDemoSkill

__all__ = ["BlogSummarizeSkill", "CreateSkillDemoSkill"]
