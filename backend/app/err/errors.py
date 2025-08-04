class SubscriptionError(Exception):
    '''Ограничение подписки'''
    pass


class MaxCategoryLevelError(Exception):
    '''Ограничение уровня вложенности категорий'''
    pass
