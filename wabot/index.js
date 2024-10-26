const fs = require('fs');
const venom = require('venom-bot');
const mime = require('mime-types');
const axios = require('axios');

const FormData = require('form-data');

const API_URL = process.env.API_URL

console.log(API_URL);

function getRandomName() {
    return Math.random().toString(36).substring(7);
}

function getImageDescription(path) {
    const formData = new FormData();
    formData.append('image', fs.createReadStream(path));
  
    return axios.post(`${API_URL}/upload-image`, formData, {
      headers: {
        ...formData.getHeaders(),
      }
    });
}

function convertAudioToText(path) {
  const formData = new FormData();
  formData.append('audio', fs.createReadStream(path));

  return axios.post(`${API_URL}/upload-audio`, formData, {
    headers: {
      ...formData.getHeaders(),
    }
  });
}

venom
  .create({
    session: 'liverbot'
  })
  .then((client) => start(client))
  .catch((erro) => {
    console.log(erro);
  });

function start(client) {
  client.onMessage(async (message) => {
    console.log(message);
    if (message.type === 'image' || message.type === 'audio' || message.type === 'ptt') {
    const buffer = await client.decryptFile(message);
    const fileName = `${getRandomName()}.${mime.extension(message.mimetype)}`;
    const path = `./media/${fileName}`;
    fs.writeFile(path, buffer, (err) => {
        if (err) {
        console.error(err);
        } else {
            const isAudio = message.mimetype.includes('audio');

            if (isAudio) {
              convertAudioToText(path).then(async (res) => {
                const description = res.data.description;
                client.sendText(message.from, `Descripción del audio: ${description}`);
              }).catch((err) => {
                console.error(err);
              });
            } else {
              getImageDescription(path).then(async (res) => {
                const description = res.data.description;
                const urlSearch = `${API_URL}/search-results?query=${encodeURIComponent(description)}`;
                console.log(urlSearch);
                await client
                    .sendText(message.from, `Buscando artículos similares a: ${description}`);
                await client.sendText(
                  message.from,
                  urlSearch
                )
              }).catch((err) => {
                console.error(err);
              });
            }
            console.log('File written successfully');
        }
    });
    }
  });
}