import random


class ReferenceStr:
    """A class to generate reference string and dirty bits."""

    def __init__(self, min=1, max=1200, length=120000, random_seed=133040007):
        """Constructor.

        Args:
            min (int, optional): Minimum page number. Defaults to 1.
            max (int, optional): Maximum page number. Defaults to 1200.
            length (int, optional): The length of reference string. Defaults to 120000.
            random_seed (int, optional): The random seed for the genertator. Defaults to 133040007.

        Raises:
            ValueError: The length of the reference string must be greater than 200.
        """
        self.min = min
        self.max = max
        self.length = length
        self.random_seed = random_seed
        self.reference_str = []
        self.dirty_bits = []

        if self.length < 200:
            raise ValueError("The length of the reference string is too short.")

    def generate_reference_str(
        self, type, locality_range_min=25, locality_range_max=100
    ):
        """
        Generate reference string based on the type.
        And also generate dirty bit for each reference.
        """
        random.seed(self.random_seed)
        self.dirty_bits = [random.choice([0, 1]) for _ in range(self.length)]

        if type == "random":
            self.reference_str = self.random_reference_str()
        elif type == "locality":
            self.reference_str = self.locality_reference_str(
                locality_range_min, locality_range_max
            )
        elif type == "my_reference_string":
            self.reference_str = self.my_reference_string()

    def random_reference_str(self):
        """Arbitrarily pick one number for each reference.

        Returns:
            list: reference string
        """
        return [random.randint(self.min, self.max) for _ in range(self.length)]

    def locality_reference_str(self, locality_range_min=25, locality_range_max=100):
        """Simulate procedure calls.

        The reference string length of each procedure call accounts for 1/200-1/100 of the
        overall reference string length.
        Note that the length shall be random.

        Returns:
            list: reference string
        """
        reference_str = []
        while len(reference_str) < self.length:
            length = random.randint(self.length // 200, self.length // 100)
            locality_range = random.randint(locality_range_min, locality_range_max)
            base_page = random.randint(self.min, self.max)

            reference_str += [
                random.randint(base_page, min(base_page + locality_range, self.max))
                for _ in range(min(length, self.length - len(reference_str)))
            ]

        return reference_str

    def my_reference_string(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        pass

    def get_reference_str(self):
        return self.reference_str.copy()

    def get_dirty_bits(self):
        return self.dirty_bits.copy()
