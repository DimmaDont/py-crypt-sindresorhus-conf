import fs from 'node:fs'

import Conf from 'conf'


const key = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
fs.writeFileSync('./key.txt', key)

const config = new Conf({
    projectName: 'foo',
    cwd: './',
    encryptionKey: key,
})
config.set({"c": 1, "b": 2, "a": 3})

fs.writeFileSync('./config_plaintext.json', config._serialize(config.store));
