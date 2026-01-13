import prisma from '../prisma/prismaClient.ts';
import { faker } from '@faker-js/faker';

async function main() {

    // Create 10 fake users
    const users = await prisma.users.createManyAndReturn({
        data: Array.from({ length: 10 }).map(() => ({
            id: faker.string.uuid(),
            email: faker.internet.email(),
            password_hash: faker.internet.password(),
            created_at: faker.date.between({ from: new Date('2025-01-01T00:00:00.000Z'), to: new Date() }), 
        })),
    });

    // Create 10 tags
    const tags = await prisma.tags.createManyAndReturn({
        data: Array.from({ length: 10 }).map(() => ({
            id: faker.string.uuid(),
            name: faker.lorem.word(),
        })),
    });

    //helper function to calculate updated_at date
    function calculateUpdatedAt(createdAt: Date){
        return faker.date.between({ from: createdAt, to: new Date() });
    };
    // Create 25 journal entries
    const journalEntries = await prisma.journal_entries.createManyAndReturn({
        data: Array.from({ length: 25 }).map(() => {
            const created_at = faker.date.between({ from: new Date('2025-01-01T00:00:00.000Z'), to: new Date() });

            return {
            id: faker.string.uuid(),
            user_id: faker.helpers.arrayElement(users).id,
            title: faker.lorem.sentence(),
            content: faker.lorem.paragraphs({ min: 1, max: 5 }),
            created_at: created_at,
            updated_at: calculateUpdatedAt(created_at),
        }})
    });



}