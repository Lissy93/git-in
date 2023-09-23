import unittest
import os

# Get the directory where the script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    # Set the start directory to the directory of this script
    test_suite = test_loader.discover(start_dir=current_directory, pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
