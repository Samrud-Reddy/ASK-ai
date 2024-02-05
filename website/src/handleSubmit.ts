export const handleSubmit = async (question: string, subject: string, prevChat: string[]): Promise<string> => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(subject);
        }, 300);
    });
};
