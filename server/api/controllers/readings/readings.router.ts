import express from 'express';
import controller from './readings.controller'
export default express.Router()
    .get('/', controller.currDay);