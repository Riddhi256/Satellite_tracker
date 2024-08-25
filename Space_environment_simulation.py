import random
import time

class SpaceEnvironment:
    def __init__(self):
        self.radiation_level = 0
        self.microgravity_effect = 0
        self.time_elapsed = 0

    def update_radiation(self):
        # Radiation can vary, e.g., from 0 to 100 units
        self.radiation_level = random.uniform(0, 100)
        print(f"Radiation level: {self.radiation_level:.2f} units")

    def update_microgravity(self):
        # In microgravity, objects experience a very small force; we'll simulate this with a small effect.
        self.microgravity_effect = random.uniform(-0.01, 0.01)
        print(f"Microgravity effect: {self.microgravity_effect:.4f}")

    def simulate_environment(self, duration_seconds, update_interval=1):
        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            self.update_radiation()
            self.update_microgravity()
            self.time_elapsed += update_interval
            time.sleep(update_interval)

    def display_summary(self):
        print(f"\nSimulation Summary:")
        print(f"Total time simulated: {self.time_elapsed} seconds")
        print(f"Final radiation level: {self.radiation_level:.2f} units")
        print(f"Final microgravity effect: {self.microgravity_effect:.4f}")

def main():
    print("Starting space environment simulation...\n")
    
    # Create a SpaceEnvironment instance
    space_env = SpaceEnvironment()
    
    # Simulate the environment for 10 seconds
    space_env.simulate_environment(duration_seconds=10)
    
    # Display the summary of the simulation
    space_env.display_summary()

if __name__ == "__main__":
    main()
