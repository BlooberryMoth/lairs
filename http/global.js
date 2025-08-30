const POST = async data => {
    let response = await fetch(".", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        }
    });
    return JSON.parse(await response.text());
};

