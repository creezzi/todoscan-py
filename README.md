# todoscan

Find TODO, FIXME and HACK comments across a codebase from the command line.

## Usage

```python
todoscan src/
todoscan . --tags TODO FIXME --strict   # exit 1 if any are found
```

## Test

```bash
pip install pytest && pytest
```

## License

MIT
