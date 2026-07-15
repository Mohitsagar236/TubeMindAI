export const uid = () => crypto.randomUUID();
export const friendlyError = (error: unknown) => error instanceof Error ? error.message : 'Something went wrong. Please try again.';
