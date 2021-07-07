import time

"""
Arguments:

1. Team interface object (t)
2. An array of flags (flags)
"""
def flag_submitter(t, flags):
    # Try submitting flags, forever
    while True:
        try:
            print(t.submit_flag(flags))
            break

        # Retry
        except Exception as e:
            print(f"Exception: {e}. Retrying.")
            time.sleep(1)
