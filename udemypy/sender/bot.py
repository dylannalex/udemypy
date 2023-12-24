from abc import ABC
from abc import abstractmethod
from udemypy.course import Course


class SenderBot(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def send_course(self, course: Course) -> None:
        pass
