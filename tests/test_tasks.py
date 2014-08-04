from unittest import TestCase


class TestFabTasks(TestCase):
    """
    Test the fabric tasks
    """

    def test_user_list(self):
        """
        We can list users
        """
        pass

    def test_add_user_by_key(self):
        """
        We can add a user using a pasted key
        """
        pass

    def test_add_user_by_path(self):
        """
        We can add a user by using a path to a key
        """
        pass

    def test_delete_user(self):
        """
        We can delete a user
        """
        pass

    def test_batch_addition(self):
        """
        We can add a list of users
        """
        pass

    def test_batch_addition_with_replace(self):
        """
        We can add a list of users, and remove unspecified users
        """
        pass

    def test_batch_addition_with_replace_and_force(self):
        """
        We are not prompted for a confirmation when used with force
        """
        pass

    def test_batch_deletion(self):
        """
        We can delete a list of users
        """
        pass

    def test_batch_deletion_with_force(self):
        """
        We are not prompted for a confirmation when used with force
        """
        pass
