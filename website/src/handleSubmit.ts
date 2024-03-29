export const handleSubmit = async (question: string, subject: string, history: string[]) => {
    try {
        const url = "http://127.0.0.1:5000/query";
        const res = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                subject: subject,
                query: question,
                history: history,
            }),
        });
        const text = await res.text();

        return text;
    } catch (e) {
        console.log(e);
        return new Error("Server Error");
    }
};
