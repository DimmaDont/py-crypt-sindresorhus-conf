import fs from "node:fs";

import Conf from "conf";

const key = fs.readFileSync("key.txt");


const config = new Conf({
  projectName: "foo",
  cwd: ".",
  encryptionKey: key,
});


fs.writeFileSync("config_plaintext.json", config._serialize(config.store));
