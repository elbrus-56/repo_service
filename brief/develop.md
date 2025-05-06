# Способы реализации бизнес-логики

1. Use Case (Application Service) как отдельный класс (текущая реализация)

``` python
class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, dto: UserCreateDTO):
        user = User(**dto.model_dump())
        await self.user_repo.save(user)
```

2. CQRS (Command Query Responsibility Segregation)
разделение операций записи и чтения

```python
# Command
class CreateOrderCommandHandler:
    def handle(self, command: CreateOrderCommand):
        ...

# Query
class GetOrderQueryHandler:
    def handle(self, query: GetOrderQuery):
        ...
```

3. Domain Events
Когда действия происходят не последовательно, а реактивно — можно использовать доменные события.

```python
class UserCreatedEvent:
    def __init__(self, user_id: UUID):
        self.user_id = user_id

# Где-то в UseCase
event_bus.publish(UserCreatedEvent(user.id))
```

4. Specification Pattern
Полезен, когда нужно динамически определять условия валидации или выборки.

```python
class UserIsEligibleForDiscount(Specification):
    def is_satisfied_by(self, user: User) -> bool:
        return user.purchase_count > 5

# Использование
if discount_spec.is_satisfied_by(user):
    apply_discount()
```

5. Strategy / Policy Pattern

Если поведение зависит от контекста или настроек — например, разные алгоритмы расчета цены.

```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, product: Product) -> Decimal:
        ...

class RegularPricing(PricingStrategy):
    ...

class DiscountedPricing(PricingStrategy):
    ...

# В UseCase
def set_pricing_strategy(self, strategy: PricingStrategy):
    self.pricing_strategy = strategy

```

6. Pipeline / Middleware Pattern

Можно обрабатывать входящие запросы через цепочку обработчиков: валидация → авторизация → логирование → сам юзкейс.

```python
class ValidationMiddleware:
    def handle(self, request, next_handler):
        validate(request)
        return next_handler(request)

class LoggingMiddleware:
    def handle(self, request, next_handler):
        log_request(request)
        return next_handler(request)
```

7. DDD (Domain-Driven Design)

8. Фасад
 паттерн Facade может быть полезен , особенно если ты хочешь скрыть сложность взаимодействия между несколькими репозиториями, сервисами или интеграциями под одним простым API.
```python

class UserFacade:
    def __init__(self, user_repo: UserRepository, analytics_repo: AnalyticsRepository):
        self.user_repo = user_repo
        self.analytics_repo = analytics_repo

    async def register_user(self, dto: UserCreateDTO) -> UUID:
        user = User(**dto.model_dump())
        await self.user_repo.save(user)
        await self.analytics_repo.log_registration(user.id)
        return user.id

class RegisterUserUseCase:
    def __init__(self, facade: UserFacade):
        self.facade = facade

    async def execute(self, dto: UserCreateDTO):
        return await self.facade.register_user(dto)

# А внутри facade:
async def register_user(...):
    # вызывает репозитории, логику, внешние службы
```
