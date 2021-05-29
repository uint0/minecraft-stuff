import functools


def require_channel(channel):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, ctx, *args, **kwargs):
            if str(ctx.channel.id) != str(channel):
                return None
            return await func(self, ctx, *args, **kwargs)
        return wrapper
    return decorator
