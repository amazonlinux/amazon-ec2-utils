# ec2-metadata regression testing

`capture-output.sh` runs every `ec2-metadata` subcommand and saves each output to a separate file. This lets you compare output before and after a code change to catch regressions.

## Usage

```bash
# 1. Capture baseline output (before your changes)
./capture-output.sh output-before

# 2. Make your changes to ec2-metadata

# 3. Capture output again
./capture-output.sh output-after

# 4. Compare
diff -r output-before output-after
```

No diff output means the change is behavior-preserving. Any differences will show exactly which subcommand's output changed and how.

## Notes

- Must be run on an EC2 instance (requires IMDS access).
- The subcommand list is derived dynamically from `ec2-metadata --help`, so new options are picked up automatically.
- Individual subcommand failures are logged as warnings but don't stop the run, so you get partial results even if some metadata categories are unavailable.
