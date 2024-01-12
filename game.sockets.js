module.exports = (io) => {
  const prover9 = require("./prover9.js");
  const buildText = require("./fileTemplate.js");
  io.on("connection", (socket) => {
    const initialGameState = {
      lives: 100,
      lost: false,
      size: 8,
      currentPosition: {
        x: 1,
        y: 1,
      },
      discovered: [],
    };

    let gameState = JSON.parse(JSON.stringify(initialGameState));

    const checkIfSafe = (coordinatesToCheck, callback) => {
      const inputTextForProver9 = buildText(
        gameState.discovered.filter((cell) => cell.type === "HINT").map((cell) => cell.value),
        coordinatesToCheck
      );
      prover9(inputTextForProver9, callback);
    };

    const updateGameState = () => {
      if (gameState.lost) return;

      const currentItem = findItemByCoordinates(gameState.currentPosition);

      if (
        currentItem &&
        !gameState.discovered.find((item) => JSON.stringify(item) === JSON.stringify(currentItem))
      ) {
        gameState.discovered.push(currentItem);

        if (currentItem && currentItem.type === "MINE") {
          gameState.lost = true;
          socket.emit("UPDATE", gameState);
          console.log(gameState)
          return;
        }

        checkIfSafe(gameState.currentPosition, (safe, error) => {
          if (!safe) {
            if (gameState.lives > 0) {
              gameState.lives -= 1;
            } else {
              gameState.lost = true;
            }
          }
          socket.emit("UPDATE", gameState);
          console.log(gameState)
        });
      }
      else{
        socket.emit("UPDATE", gameState);
      }
    };

    updateGameState();

    socket.on("RESTART", () => {
      gameState = JSON.parse(JSON.stringify(initialGameState));
      updateGameState();
    });

    socket.on("KEY_EVENT", (key) => {
      switch (key) {
        case "ArrowUp":
          if (gameState.currentPosition.x > 1) {
            gameState.currentPosition.x--;
            updateGameState();
          }
          break;
        case "ArrowDown":
          if (gameState.currentPosition.x < 8) {
            gameState.currentPosition.x++;
            updateGameState();
          }
          break;
        case "ArrowLeft":
          if (gameState.currentPosition.y > 1) {
            console.log("clicked")
            gameState.currentPosition.y--;
            updateGameState();
          }
          break;
        case "ArrowRight":
          if (gameState.currentPosition.y < 8) {
            gameState.currentPosition.y++;
            updateGameState();
          }
          break;
        default:
          break;
      }
    });
  });
};

const findItemByCoordinates = ({ x, y }) => {
  const items = require("./items");
  let found = {
    coordinates: { x, y },
    type: "EMPTY",
    value: "",
  };
  items.forEach((item) => {
    if (JSON.stringify(item.coordinates) === JSON.stringify({ x, y })) {
      found = item;
    }
  });
  return found;
};