module.exports = (content, callback) => {
    const fs = require("fs");
    const { exec } = require("child_process");
    const date = new Date();
    const fileName = `./prover_files/out_${date.getTime()}.txt`
    try {
      fs.writeFileSync(fileName, content);
  
      exec("prover9 -f "+fileName, (error, stdout, stderr) => {
        if (stderr && !(stdout.includes("Exiting with failure."))) {
          console.log("stdout",stdout);
          callback(true, null);
          return;
        }
  
    
        if (error) {
          console.log("SEARCH_FAILED");
          callback(false, error);
          return;
        }
  
        console.log("NOTHING");
        callback(false, null);
        return;
      });
      
    } catch (error) {
      console.log("CAUGHT_ERROR");
      callback(true, null);
    }
  };