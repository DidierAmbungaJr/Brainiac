import os
import uuid
import requests

import streamlit as st

from src.multi_agent import create_report_orchestrator, create_team
from src.conversation_report import (
    generate_conversation_report,
    format_transcript,
    report_to_markdown,
    report_to_json,
)
from src.response import invoke_agent


st.set_page_config(page_title="Brainiac", page_icon="🧠", layout="centered")
st.title("Brainiac")
st.caption("Superviseur Gemini et agent de recherche spécialisé")
st.caption(f"Modèle : `{os.getenv('GEMINI_MODEL', 'gemini-3.6-flash')}`")


def get_agent():
    if "agent" not in st.session_state:
        session_id = f"streamlit_{uuid.uuid4().hex}"
        st.session_state.agent = create_team(session_id=session_id)
    return st.session_state.agent


def get_report_orchestrator():
    if "report_orchestrator" not in st.session_state:
        st.session_state.report_orchestrator = create_report_orchestrator()
    return st.session_state.report_orchestrator


if not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
    st.error("Configurez GOOGLE_API_KEY ou GEMINI_API_KEY dans votre fichier .env.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_tab, report_tab = st.tabs(["Discussion", "Rapport terrain"])

with chat_tab:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("thinking"):
                with st.expander("Thinking", expanded=False):
                    st.markdown(message["thinking"])
            st.markdown(message["content"])

    if prompt := st.chat_input("Posez une question à Brainiac..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    output = invoke_agent(get_agent(), prompt)
                if output.thinking:
                    with st.expander("Thinking", expanded=False):
                        st.markdown(output.thinking)
                st.markdown(output.response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": output.response, "thinking": output.thinking}
                )
            except Exception as error:
                st.error(f"Erreur pendant l'appel de l'agent : {error}")

with report_tab:
    st.subheader("Rapport de visite commerciale")
    st.caption("Collez ici le transcript produit par votre modèle TTS.")
    transcript = st.text_area(
        "Transcript",
        value=st.session_state.get("transcript", ""),
        height=280,
        placeholder="Commercial : ...\nClient : ...",
    )
    st.session_state.transcript = transcript

    if st.button("Générer le rapport", type="primary"):
        try:
            with st.spinner("L'orchestrateur délègue l'analyse au rapporteur..."):
                st.session_state.conversation_report = generate_conversation_report(
                    transcript,
                    agent=get_report_orchestrator(),
                )
                st.session_state.report_markdown = report_to_markdown(
                    st.session_state.conversation_report
                )
        except Exception as error:
            st.error(f"Erreur pendant la génération du rapport : {error}")

    if "conversation_report" in st.session_state:
        st.divider()
        st.subheader("Relecture commerciale")
        edited_markdown = st.text_area(
            "Document Markdown éditable",
            value=st.session_state.get("report_markdown", ""),
            height=360,
        )
        st.session_state.report_markdown = edited_markdown
        approved = st.checkbox("Je valide ce rapport pour envoi au supérieur")
        report_json = report_to_json(st.session_state.conversation_report)
        st.download_button(
            "Télécharger le JSON validé",
            data=report_json if approved else "",
            file_name="conversation_report.json",
            mime="application/json",
            disabled=not approved,
        )
        st.download_button(
            "Télécharger le document Markdown",
            data=edited_markdown if approved else "",
            file_name="conversation_report.md",
            mime="text/markdown",
            disabled=not approved,
        )
        backend_url = os.getenv("DJANGO_REPORT_URL")
        if backend_url and st.button("Envoyer au backend Django", disabled=not approved):
            response = requests.post(backend_url, json=st.session_state.conversation_report, timeout=20)
            if response.ok:
                st.success("Rapport envoyé au backend Django.")
            else:
                st.error(f"Le backend a répondu {response.status_code}.")