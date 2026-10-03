import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.95.3";

const corsHeaders = {
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Origin": "*",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });
}

Deno.serve(async (request) => {
  if (request.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  if (request.method !== "POST") return json({ error: "Méthode non autorisée." }, 405);

  const publishableKeys = JSON.parse(Deno.env.get("SUPABASE_PUBLISHABLE_KEYS") ?? "{}");
  const client = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    publishableKeys.default ?? Deno.env.get("SUPABASE_ANON_KEY") ?? "",
  );

  const { question } = await request.json().catch(() => ({}));
  if (typeof question !== "string" || !question.trim()) return json({ error: "Question manquante." }, 400);

  const { data: items, error: itemsError } = await client
    .from("base_connaissances")
    .select("*")
    .order("id");
  if (itemsError) return json({ error: "Lecture de la base impossible." }, 500);

  const words = question.toLocaleLowerCase().match(/[\p{L}\p{N}]{3,}/gu) ?? [];
  const matchingItems = (items ?? []).filter((item) => {
    const searchable = [item.Nom, item["Note Alex"], item.Texte, item["Étiquettes"]]
      .join(" ")
      .toLocaleLowerCase();
    return words.some((word) => searchable.includes(word));
  }).slice(0, 12);
  if (!matchingItems.length) {
    return json({ answer: "Je ne trouve aucune fiche correspondant aux mots de cette question.", sources: [] });
  }

  const context = matchingItems.map((item) => ({
    id: item.id,
    nom: item.Nom || "Sans titre",
    note: item["Note Alex"] || "",
    texte: item.Texte || "",
    etiquettes: item["Étiquettes"] || "",
  }));
  const apiKey = Deno.env.get("API_1") ?? Deno.env.get("GEMINI_API_KEY");
  if (!apiKey) return json({ error: "La clé Gemini API_1 est absente des secrets Supabase." }, 500);

  const prompt = `Tu es le chatbot d'une base de connaissances. Réponds uniquement avec les informations présentes dans les fiches ci-dessous. Si elles ne permettent pas de répondre, dis-le clairement. Réponds en français, avec une réponse courte et utile. À la fin, ajoute une ligne SOURCES: suivie des identifiants des fiches utilisées, séparés par des virgules.\n\nQUESTION: ${question.trim()}\n\nFICHES PERTINENTES :\n${JSON.stringify(context)}`;
  const response = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent", {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": apiKey },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { temperature: 0.2 } }),
  });
  if (!response.ok) return json({ error: `Gemini n'a pas pu répondre (code ${response.status}).` }, 502);

  const gemini = await response.json();
  const raw = gemini.candidates?.[0]?.content?.parts?.[0]?.text ?? "Aucune réponse fournie.";
  const sourceMatch = raw.match(/\n?SOURCES:\s*(.*)$/i);
  const ids = sourceMatch ? [...sourceMatch[1].matchAll(/\d+/g)].map((match) => Number(match[0])) : [];
  const sources = context.filter((item) => ids.includes(item.id)).map((item) => `${item.id} — ${item.nom}`);
  return json({ answer: raw.replace(/\n?SOURCES:\s*.*$/i, "").trim(), sources });
});
