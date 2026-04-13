"""
Monkey patch: preserve cache_control for DashScope provider.

LiteLLM's OpenAIGPTConfig base class strips cache_control by default.
DashScope supports cache_control for prompt caching, so we override
to preserve it (same pattern as ZAI/MiniMax/Databricks providers).

Refs:
- https://github.com/BerriAI/litellm/issues/18165
- https://github.com/BerriAI/litellm/pull/22254
- https://help.aliyun.com/zh/model-studio/context-cache
"""

import logging

logger = logging.getLogger(__name__)


def apply():
    from litellm.llms.dashscope.chat.transformation import DashScopeChatConfig

    if "remove_cache_control_flag_from_messages_and_tools" in DashScopeChatConfig.__dict__:
        logger.info(
            "[patch] DashScope already overrides remove_cache_control_flag_from_messages_and_tools, "
            "skipping patch (upstream may have fixed https://github.com/BerriAI/litellm/issues/18165)"
        )
        return

    def remove_cache_control_flag_from_messages_and_tools(self, model, messages, tools=None):
        """Override to preserve cache_control for DashScope."""
        return messages, tools

    DashScopeChatConfig.remove_cache_control_flag_from_messages_and_tools = (
        remove_cache_control_flag_from_messages_and_tools
    )
    logger.info("[patch] DashScope cache_control preservation enabled")
