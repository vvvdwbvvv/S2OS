CC = x86_64-linux-musl-gcc
CFLAGS = -static -Os
SRC = vuln_buffer.c
TARGET = vuln_buffer


OUT_DIR = ../app
BIN = $(OUT_DIR)/$(TARGET)

all: $(BIN)

$(BIN): $(SRC)
	@mkdir -p $(OUT_DIR)
	@echo "[🔨] compile $(SRC) → $(BIN)"
	$(CC) $(CFLAGS) -o $(BIN) $(SRC)
	@chmod +x $(BIN)
	@echo "[✅] compile finished, export to $(BIN)"

clean:
	@rm -f $(BIN)
	@echo "[🧹] clean result"

.PHONY: all clean
