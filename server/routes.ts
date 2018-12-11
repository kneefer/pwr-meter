import { Application } from 'express';
import examplesRouter from './api/controllers/examples/router'
import readingsRouter from './api/controllers/readings/readings.router'
export default function routes(app: Application): void {
  app.use('/api/v1/examples', examplesRouter);
  app.use('/api/v1/readings', readingsRouter);
};