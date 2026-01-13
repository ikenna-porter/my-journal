import express from 'express';

const router = express.Router();

router.get('/', async (req, res, next) => {

})

router.get('/:id', async (req, res, next) => {
})

router.post('/:id', async (req, res, next) => {
    console.log('method:',req.method);
    console.log('body:', req.body);
    // return res.status(201).json({ message: 'Entry created successfully' });
})

router.put('/:id', async (req, res, next) => {})

router.delete('/:id', async (req, res, next) => {})

export default router;