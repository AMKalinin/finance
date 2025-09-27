class SubscriptionError(Exception):
    '''Ограничение подписки'''
    pass


class MaxCategoryLevelError(Exception):
    '''Ограничение уровня вложенности категорий'''
    pass

class CreateCategoryError(Exception):
    '''Ошибка при создании категории'''
    pass
