import express from 'express';
import multer from 'multer';
import axiosFormData from 'axios-form-data';
import axios from 'axios';
import fs from "fs";
import QRImage from 'qr-image';
import sharp from 'sharp';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json())

// Set up storage configuration for Multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
      cb(null, 'uploads/'); // Specify the directory to save files
  },
  filename: (req, file, cb) => {
      cb(null, file.originalname); // Use the original file name
  }
});

// Initialize Multer with the storage configuration
const upload = multer({ storage: storage });

// connect axiosFormData interceptor to axios
axios.interceptors.request.use(axiosFormData);

// compare
app.post('/v1/best-shots', upload.array('image', 5), async (req, res) => {
    try {
      console.log(req.files)
      console.log(req.body.query)
  
      const promptPromises = req.files.map(async (val) => {
        const options = {
          method: 'POST',
          url: 'http://localhost:5000/detect',
          headers: {
            "Content-Type": "multipart/form-data"
          },
          data: {
            query: `${req.body.query}`,
            image: fs.createReadStream(`uploads/${val.filename}`)
          }
        };

        const resp = await axios.request(options)
        return {answer: resp.data.answer, filename: val.filename }
      })

      const detectResult = await Promise.all(promptPromises)
      const existResult = detectResult.filter((arr) => { return arr.answer.length > 0 } )
      if(existResult.length == 1) {
        res.status(200).json({success: true, filename: existResult[0].filename});
        return
      }

      if(existResult.length > 1) {
        let smallestPoint = parseFloat(existResult[0].answer[0].x_max) - parseFloat(existResult[0].answer[0].x_min)
        let smallestFilename = existResult[0].filename
        for(let i=0;i<existResult.length;i++) {
          if(i == 0) continue;
          const data = existResult[i]
          const minPoint = parseFloat(data.answer[0].x_max) - parseFloat(data.answer[0].x_min)
          if(minPoint < smallestPoint) {
            smallestPoint = minPoint
            smallestFilename = data.filename
          }
        }
        res.status(200).json({success: true, filename: smallestFilename});
        return
      }
  
      res.status(400).json({success: false, message: 'no picture match your query'});
    }catch(err) {
      console.error(err)
    }
});

app.post('/v1/generate-qr', async (req, res) => {
  try {
    const data = JSON.stringify(req.body.data)
    const generated = QRImage.imageSync(data, {type: 'png'})
    const img = Buffer.from(generated)
    res.writeHead(200, {
      'Content-Type': 'image/png',
      'Content-Length': img.length
    });
    res.end(img); 
  }catch(err) {
    console.error(err)
  }
})

app.post('/v1/before-after', upload.array('image', 2), async (req, res) => {
  try {
    console.log(req.files)

    await mergeImages(req.files[0].path, req.files[1].path)

    const options = {
      method: 'POST',
      url: 'http://localhost:5000/query',
      headers: {
        "Content-Type": "multipart/form-data"
      },
      data: {
        query: `find differences between these 2 photos`,
        image: fs.createReadStream(`uploads/merged.png`)
      }
    };

    const resp = await axios.request(options)
    res.status(200).json({success: true, message: resp.data.answer})

  }catch(err) {
    console.error(err)
  }
})

async function mergeImages(imagePath1, imagePath2) {
  try {
    const metadata1 = await sharp(imagePath1).metadata();
    const metadata2 = await sharp(imagePath2).metadata();

    return await sharp({
      create: {
        width: metadata1.width + metadata2.width,
        height: Math.max(metadata1.height, metadata2.height),
        channels: 3,
        background: { r: 0, g: 0, b: 0 }
      }
    })
      .composite([
        { input: imagePath1, gravity: 'west' },
        { input: imagePath2, gravity: 'east' }
      ])
      .toFile('uploads/merged.png')
  } catch (error) {
    console.error('Error merging images:', error);
  }
}

app.post('/v1/happiness', upload.array('image', 5), async (req, res) => {
  try {
    console.log(req.files)
    console.log(req.body.query)

    const promptPromises = req.files.map(async (val) => {
      const options = {
        method: 'POST',
        url: 'http://localhost:5000/detect',
        headers: {
          "Content-Type": "multipart/form-data"
        },
        data: {
          query: `smile`,
          image: fs.createReadStream(`uploads/${val.filename}`)
        }
      };

      const resp = await axios.request(options)
      return {answer: resp.data.answer, filename: val.filename }
    })

    const detectResult = await Promise.all(promptPromises)
    const existResult = detectResult.filter((arr) => { return arr.answer.length > 0 } )
    if(existResult.length == 1) {
      res.status(200).json({success: true, filename: existResult[0].filename, score: 100});
      return
    }

    if(existResult.length > 1) {
      
      const ratePromises = existResult.map(async (val) => {
        const options = {
          method: 'POST',
          url: 'http://localhost:5000/query',
          headers: {
            "Content-Type": "multipart/form-data"
          },
          data: {
            query: `rate the happiness of the visitors!`,
            image: fs.createReadStream(`uploads/${val.filename}`)
          }
        };
  
        const resp = await axios.request(options)
        const score = resp.data.answer.match(pattern)[0]
        return {answer: resp.data.answer, filename: val.filename, score: score ? score : 0 }
      })

      const rateResult = await promise.all(ratePromises)
      let biggest = rateResult[0]
      for(const val of rateResult) {
        if(val.score > biggest.score) {
          biggest = val
        }
      }

      res.status(200).json({success: true, filename: biggest.filename, score: biggest.score});
      return
    }

    res.status(400).json({success: false, message: 'no picture match your query'});
  }catch(err) {
    console.error(err)
  }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
