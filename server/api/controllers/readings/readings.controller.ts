import { Request, Response } from 'express';
import fs from 'fs';
import path from 'path';
import csvParse from 'csv-parse';
import { promisify } from 'util';

const readdir = promisify(fs.readdir);
const readfile = promisify(fs.readFile);

const readingsRelativePath = '../../../../rpi/readings';

export class ReadingsController {
  async currDay(req: Request, res: Response) {
    res.setHeader('Content-Type', 'application/json');

    const readingsAbsolutePath = path.join(__dirname, readingsRelativePath);
    const files = await readdir(readingsAbsolutePath);
    const newestDayFile = files.sort().reverse()[0];
    const fileContent = await readfile(`${readingsAbsolutePath}/${newestDayFile}`, 'utf8');
    csvParse(fileContent, { delimiter: ',', }, function(err, output) {
      const dataParsed = output.map(x => ({date: x[0], totalPulses: x[1]}))
      res.json(dataParsed);
    });
  }
}
export default new ReadingsController();