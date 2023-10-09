// convert data into html
const create_html = (d) => {
    let url = d.url;
    let labels = d.labels
        .map(d => `<span onclick="change(this.innerText)">${d}</span>`)
        .join(" ");
    let name = d.name;
    return `
<div onclick="goto_url(this)" title="${url}">
    <div class="name">
        <i>${labels}</i>
        <div>${name}</div>
    </div>
    <a href="${url}" target="_blank">前往</a>
</div>`;
}

// jump to tool
const goto_url = (el) => {
    el.querySelector("a").click();
};

// when search bar value change, redirect the website
const change = (keyword) => {
    document.location.search = `?q=${keyword}`;
}

// get search value from the message in url
const load_search_value = () => {
    let keyword = "";
    document.location.search.slice(1).split("&").forEach(e => {
        let ts = e.split("=", 2);
        let k = ts[0];
        let v = decodeURIComponent(ts[1]);
        if (k == "q") keyword = v;
    });
    search.value = keyword;
}

const filter_by_keywords = (data, keywords) => {
    return data
        .filter(d => {
            let s = `${d.labels} ${d.name} ${d.url}`;
            let flag = true;
            keywords.forEach(k => {
                if (s.indexOf(k) < 0) flag = false;
            });
            return flag;
        });
}

const load_tools = async (cache) => {
    const res = await fetch("tools.json", { cache });
    const data = await res.json();
    const keywords = search.value.split(" ");
    const data2 = filter_by_keywords(data, keywords);
    const text = data2.map(d => create_html(d)).join("\n");
    return tools.innerHTML = text;
}

const check_update = (update_time) => {
    let old_time = localStorage.getItem("update_time");
    if (!old_time) return true;
    return Number(old_time) == update_time;
}

const init = async () => {
    load_search_value();

    const res = await fetch("config.json", { cache: "reload" });
    const data = await res.json();

    let cache = "default";
    let update_time = data.update_time;
    update.innerHTML = new Date(update_time);
    if (check_update(update_time)) cache = "reload";
    await load_tools(cache);
    localStorage.setItem("update_time", String(update_time));
}

init();
