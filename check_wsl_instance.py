import subprocess

# # Run the 'wsl -l -v' command
# result = subprocess.run(
#     ["wsl", "-l", "-v"],
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     text=True
# )

# # Get the list of existing instances
# existing_instances = result.stdout.strip()  # Remove leading/trailing whitespace and newlines

# # Remove null characters (\x00) from the output
# cleaned_instances = existing_instances.replace('\x00', '')

# # Print the cleaned output for debugging
# print(f"Cleaned output:\n{repr(cleaned_instances)}")

instance_name = 'cloudbook'

# # Check if the instance name exists in the cleaned output
# print(instance_name in cleaned_instances)
# if instance_name in cleaned_instances:
#     print(f"instance_name '{instance_name}' found in the string.")
# else:
#     print(f"instance_name '{instance_name}' not found in the string.")


result = subprocess.run(
            ["wsl", "-l", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

existing_instances = result.stdout.strip()
existing_instances = existing_instances.replace('\x00', '')
print()