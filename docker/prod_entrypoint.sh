#!/bin/sh

# Apply custom patches via startup hooks
# Ref: https://github.com/BerriAI/litellm/issues/18165
if [ -z "$LITELLM_WORKER_STARTUP_HOOKS" ]; then
    export LITELLM_WORKER_STARTUP_HOOKS="patches.dashscope_cache_control:apply"
else
    export LITELLM_WORKER_STARTUP_HOOKS="${LITELLM_WORKER_STARTUP_HOOKS},patches.dashscope_cache_control:apply"
fi

if [ "$USE_DDTRACE" = "true" ]; then
    export DD_TRACE_OPENAI_ENABLED="False"
    exec ddtrace-run litellm "$@"
else
    exec litellm "$@"
fi
