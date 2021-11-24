class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        mean_speed = self.get_mean_speed()
        duration_in_min = self.duration * 60
        spent_calories = (
            (coeff_calorie_1 * mean_speed - coeff_calorie_2)
            * self.weight
            / self.M_IN_KM
            * duration_in_min
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_3 = 0.035
        coeff_calorie_4 = 0.029
        mean_speed = self.get_mean_speed()
        duration_in_min = self.duration * 60
        spent_calories = (
            coeff_calorie_3 * self.weight
            + (mean_speed ** 2 // self.height) * coeff_calorie_4 * self.weight
        ) * duration_in_min
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self):
        spent_calories = (
            (self.get_mean_speed() + self.coeff_calorie_5)
            * self.coeff_calorie_6
            * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_sports = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}

    if workout_type == "SWM":
        return dict_sports["SWM"](
            action=data[0],
            duration=data[1],
            weight=data[2],
            length_pool=data[3],
            count_pool=data[4],
        )
    elif workout_type == "RUN":
        return dict_sports["RUN"](
            action=data[0], duration=data[1], weight=data[2]
        )
    elif workout_type == "WLK":
        return dict_sports["WLK"](
            action=data[0], duration=data[1], weight=data[2], height=data[3]
        )


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
