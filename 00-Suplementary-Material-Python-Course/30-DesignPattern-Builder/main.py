# The Builder pattern is a well-known pattern in Python world. 
# It’s especially useful when you need to create an object 
# with lots of possible configuration options.

# The Builder pattern can be recognized in a class, which has a single 
# creation method and several methods to configure the resulting object. 
# Builder methods often support chaining 
# (for example, someBuilder.setValueA(1).setValueB(2).create()).

# Conceptual Example: This example illustrates the structure of the Builder design pattern. It focuses on answering these questions:
    # What classes does it consist of?
    # What roles do these classes play?
    # In what way the elements of the pattern are related?

# https://refactoring.guru/design-patterns/catalog

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class Builder(ABC):
    """
    The Builder interface specifies methods for 
    creating the different parts of the Product objects.
    """

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass

class ConcreteBuilder1(Builder):
    """
    The Concrete Builder class follow Builder interface and provide
    specific implementation of building steps.
    """

    def __init__(self) -> None:
        """
        A builder instance should have a blank product object, 
        used in further assembly.
        """
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    
    @property
    def product(self) -> Product1:
        """
        Concrete Builders are supposed to provide their own methods
        for retrieving results. Various types of Builders create
        different products that don't follow the same interface.
        After returning the result to the client, a builder is 
        ready to start producing another product, therefore, it 
        is usual to call the reset method at the end of the 
        'getProduct' method body.
        """

        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.add("PartA1")

    def produce_part_b(self) -> None:
        self._product.add("PartB1")

    def produce_part_c(self) -> None:
        self._product.add("PartC1")

class Product1():
    """
    Use Builder only when products require extensive configuration.
    Concrete Builders can create unrelated products
    """

    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"Product parts: {', '.join(self.parts)}", end="")


class Director:
    """
    The Director execute the building step in a particular sequence.
    Helpful when producing products in a specific order or configuration.
    """
    def __init__(self) -> None:
        self._builder = None
    
    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        Director works with any builder instance that client code 
        pass to it. Threfore, the client code may alter the final 
        type of the newly assembled product
        """
        self._builder = builder

    
    """
    The Director can construct several product variations using
    the same building steps.
    """

    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()

    def build_full_featured_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()


if __name__ == "__main__":
    """
    The client code creates a builder object, 
    passes it to the director, and
    initiate the construction process.
    The results is retrieved from the builder object.
    """

    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder

    print("Standard basic product: ")
    director.build_minimal_viable_product()
    builder.product.list_parts()

    print("\n")

    print("Standard full featured product: ")
    director.build_full_featured_product()
    builder.product.list_parts()

    print("\n")

    # The Builder pattern can be used without a Director class
    print("Custom product: ")
    builder.produce_part_a()
    builder.produce_part_b()
    builder.product.list_parts()