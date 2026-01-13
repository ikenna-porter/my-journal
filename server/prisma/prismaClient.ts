import { PrismaClient } from './generated/client.ts'
import { PrismaPostgresAdapter } from '@prisma/adapter-ppg'

const adapter = new PrismaPostgresAdapter({ 
  connectionString: process.env.DATABASE_URL ?? ''
});

const prisma = new PrismaClient({adapter})

export default prisma; 