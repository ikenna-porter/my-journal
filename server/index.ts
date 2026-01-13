import express from 'express';
import 'dotenv/config';
import entryRoutes from './src/routes/entryRoutes.ts';

const app = express();
const PORT = Number(process.env.PORT) || 3000;

app.use(express.urlencoded({ extended: true }));
app.use('/entries', entryRoutes)


app.listen(PORT, () => {console.log(`Server is running on port ${PORT}`);});
export { app };

