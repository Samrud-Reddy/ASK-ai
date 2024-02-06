export const handleSubmit = async (question: string, subject: string) => {
    const url = "";
    const res = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            subject: subject,
            query: question,
        }),
    });

    // this should be of type {subject: "something", query: "something"}
    const json = await res.json();
    return json;
};
