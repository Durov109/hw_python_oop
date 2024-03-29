from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Type, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: int = " "
    duration: float = 0.0
    distance: float = 0.0
    speed: float = 0.0
    calories: float = 0.0

    MESS_TRAINING: ClassVar[str] = ("Тип тренировки: {training_type}; "
                                    "Длительность: {duration:.3f} ч.; "
                                    "Дистанция: {distance:.3f} км; "
                                    "Ср. скорость: {speed:.3f} км/ч; "
                                    "Потрачено ккал: {calories:.3f}.")

    def get_message(self):
        return self.MESS_TRAINING.format(**asdict(self))


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOURS: int = 60
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """
        action: количество совершённых действий число шагов,беге либо гребков
        duration: длительность тренировки
        weight: вес спортсмена
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    RUN_COEFF_CALORIE_1 = 18
    RUN_COEFF_CALORIE_2 = 20
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        return ((self.RUN_COEFF_CALORIE_1 * self.get_mean_speed()
                 - self.RUN_COEFF_CALORIE_2) * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOURS)


class SportsWalking(Training):
    WLK_COEFF_CAL_1 = 0.035
    WLK_COEFF_CAL_2 = 0.029
    """Тренировка: спортивная ходьба."""

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WLK_COEFF_CAL_1 * self.weight
                 + (self.get_mean_speed()**2
                    // self.height) * self.WLK_COEFF_CAL_2
                 * self.weight) * self.duration
                * self.MIN_IN_HOURS)


class Swimming(Training):
    SWM_COEFF_CALORIE_1 = 1.1
    SWM_COEFF_CALORIE_2 = 2
    LEN_STEP = 1.38  # переопределение длины гребка, вместо длины шага
    """Тренировка: плавание."""

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Формула для расчёта израсходованных калорий."""
        return (
            (self.get_mean_speed() + self.SWM_COEFF_CALORIE_1)
            * self.SWM_COEFF_CALORIE_2 * self.weight
        )

    def get_mean_speed(self) -> float:
        """Формула расчёта средней скорости при плавании."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training: Dict[str, Type[Training]] = {"SWM": Swimming,
                                           "RUN": Running,
                                           "WLK": SportsWalking}
    if workout_type not in training:
        raise ValueError(f"Тип тренировки {workout_type} не определен.")
    return training[workout_type](*data)


def main(training: Training):
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
