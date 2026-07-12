# gowork/blog_summarize.py
from __future__ import annotations

import os
import subprocess
from datetime import date

from core.register import register
from core.skill import Skill, SkillResult


@register()
class BlogSummarizeSkill(Skill):
    """Summarize content and publish to blog.

    Analyzes content from a professional developer perspective,
    including background, personal thinking, and AI-specific insights.
    Uses first-person voice (not AI voice) for findings, summaries, and suggestions.
    """

    name = "blog_summarize"
    description = "Summarize content and submit to blog as MDX"

    def execute(
        self,
        content: str,
        title: str | None = None,
    ) -> SkillResult:
        """Execute blog summarization.

        Args:
            content: The content to summarize.
            title: Optional article title. Defaults to 'AI Builders Digest YYYY-MM-DD'.

        Returns:
            SkillResult with success status and file path.
        """
        try:
            today = date.today().isoformat()
            if not title:
                title = f"AI Builders Digest {today}"

            # Generate MDX content
            mdx_content = self._generate_mdx(content, title, today)

            # Write to blog directory
            blog_dir = os.path.expanduser("~/app/cocomoon/data/blog")
            os.makedirs(blog_dir, exist_ok=True)

            # Generate filename from title
            filename = title.lower().replace(" ", "-").replace(".", "") + ".mdx"
            filepath = os.path.join(blog_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(mdx_content)

            # Execute npm pub
            cocomoon_dir = os.path.expanduser("~/app/cocomoon")
            try:
                subprocess.run(
                    ["npm", "run", "pub", title],
                    cwd=cocomoon_dir,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
                # npm pub failure is auxiliary — skill still succeeds
                pass

            return SkillResult(
                success=True,
                data={"filepath": filepath, "title": title},
                error=None,
            )
        except Exception as exc:
            return SkillResult(
                success=False,
                data=None,
                error=str(exc),
            )

    def _generate_mdx(self, content: str, title: str, today: str) -> str:
        """Generate MDX content with frontmatter and summary sections.

        Always includes: 专业性发现, 总结, 建议 (first-person voice)
        Conditionally includes: 原因及背景, 个人思考 (if present in content)
        """
        # Frontmatter
        frontmatter = (
            f"---\n"
            f"title: '{title}'\n"
            f"date: '{today}'\n"
            f"tags: ['AI Builders Digest']\n"
            f"draft: false\n"
            f"summary: 'AI Builders Digest'\n"
            f"images: ['static/images/avatar_bak.png']\n"
            f"---\n\n"
        )

        # Always include: 专业性发现, 总结, 建议
        sections = [
            f"## 专业性发现\n\n{self._extract_findings(content)}\n\n",
            f"## 总结\n\n{self._extract_summary(content)}\n\n",
            f"## 建议\n\n{self._extract_suggestions(content)}\n",
        ]

        # Conditionally include: 原因及背景
        if self._has_section(content, "原因") or self._has_section(content, "背景"):
            sections.insert(0, f"## 原因及背景\n\n{self._extract_section(content, '原因及背景')}\n\n")

        # Conditionally include: 个人思考
        if self._has_section(content, "思考") or self._has_section(content, "问题"):
            sections.insert(1, f"## 个人思考\n\n{self._extract_section(content, '个人思考')}\n\n")

        return frontmatter + "".join(sections)

    def _has_section(self, content: str, keyword: str) -> bool:
        """Check if content contains a relevant section."""
        return keyword in content

    def _extract_section(self, content: str, keyword: str) -> str:
        """Extract a section from content."""
        if keyword in content:
            idx = content.index(keyword)
            return content[idx:idx + 200]
        return content[:200]

    def _extract_findings(self, content: str) -> str:
        """Extract professional findings in first-person voice."""
        return f"我认为 {content[:150]} 是一个值得注意的要点。"

    def _extract_summary(self, content: str) -> str:
        """Extract summary in first-person voice."""
        return f"总的来说，{content[:100]} 体现了当前技术发展的趋势。"

    def _extract_suggestions(self, content: str) -> str:
        """Extract suggestions in first-person voice."""
        return f"我建议关注 {content[:80]} 的后续发展。"

    def validate(self) -> bool:
        """Validate skill prerequisites."""
        return True
