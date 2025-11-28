import os
import logging
from typing import Optional

# Gemini API (API key mode)
try:
    from google import genai  # type: ignore
except ImportError:
    genai = None

# Vertex AI Generative Models (service account / ADC mode)
try:
    from vertexai import init as vertexai_init  # type: ignore
    from vertexai.generative_models import GenerativeModel  # type: ignore
except ImportError:
    vertexai_init = None
    GenerativeModel = None


    logger = logging.getLogger(__name__)


class GenAIClient:
    """Flexible client that prefers service account (Vertex AI) if available, else Gemini API key.

    Precedence:
    1. If GOOGLE_APPLICATION_CREDENTIALS is set & vertexai library available -> use Vertex AI GenerativeModel.
    2. Else if GOOGLE_API_KEY is set & google.genai available -> use genai.Client.
    3. Else -> no client (summaries disabled).
    """

    def __init__(self, model: str):
        self.model = model
        self._client = None         # primary backend client (vertex preferred)
        self._gemini_client = None  # secondary gemini client if API key provided
        self.backend = None         # active backend used for first attempt ("vertex" | "gemini" | None)
        self._debug = os.getenv("LLM_DEBUG", "0") in ("1", "true", "True")
        self.resolved_model = None  # actual model that produced content

        svc_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        api_key = os.getenv("GOOGLE_API_KEY")
        project_id = os.getenv("GOOGLE_PROJECT_ID") or os.getenv("PROJECT_ID") or os.getenv("GCP_PROJECT") or "gagenteducation"
        location = os.getenv("GOOGLE_LOCATION") or "us-central1"
        
        # Attempt Vertex AI (works on Cloud Run with ADC, or with service account)
        if vertexai_init and GenerativeModel:
            try:
                vertexai_init(project=project_id, location=location)
                self._client = GenerativeModel(self.model)
                self.backend = "vertex"
                # Vertex succeeded, skip Gemini API
            except Exception:
                self._client = None
                self.backend = None
        
        # Fallback to Gemini API key mode (only if Vertex failed AND API key present)
        if not self.backend and api_key and genai:
            try:
                pass
                self._gemini_client = genai.Client(api_key=api_key)
                self._client = self._gemini_client
                self.backend = "gemini"
                pass
            except Exception:
                pass
                self._client = None
                self.backend = None
        # If vertex failed but gemini client exists and backend not set, promote gemini
        if self.backend is None and self._gemini_client is not None:
            self._client = self._gemini_client
            self.backend = "gemini"
        if self._debug:
            pass

    def summarize(self, prompt: str) -> Optional[str]:
        if not self._client and not self._gemini_client:
            pass
            return None
        pass
        
        try:
            if self.backend == "vertex":
                pass
                try:
                    resp = self._client.generate_content(prompt)
                except Exception:
                    if self._debug:
                        pass
                    resp = None
                text_out = None
                if resp is not None:
                    # Newer SDK: direct text
                    if hasattr(resp, "text") and resp.text:
                        text_out = resp.text
                    elif getattr(resp, "candidates", None):
                        try:
                            for c in resp.candidates:
                                content = getattr(c, "content", None)
                                if content and getattr(content, "parts", None):
                                    for p in content.parts:
                                        pt = getattr(p, "text", None)
                                        if pt:
                                            text_out = pt
                                            break
                                    if text_out:
                                        break
                        except Exception:
                            if self._debug:
                                pass
                if text_out:
                    self.resolved_model = self.model
                    return text_out
                # Attempt alternate Vertex models (404 or empty response) before Gemini fallback
                alt_models_env = os.getenv("ALT_MODELS")
                if alt_models_env:
                    alt_models = [m.strip() for m in alt_models_env.split(",") if m.strip()]
                else:
                    alt_models = [
                        "gemini-2.5-flash-lite",
                        "gemini-1.5-flash-002",
                        "gemini-1.5-flash-001",
                        "gemini-1.5-pro-002",
                    ]
                tried = []
                if self._debug:
                    pass
                for alt in alt_models:
                    if alt == self.model:
                        continue
                    tried.append(alt)
                    try:
                        from vertexai.generative_models import GenerativeModel as _GM
                        alt_client = _GM(alt)
                        alt_resp = alt_client.generate_content(prompt)
                        # Each alt_resp attempt leverage same parsing
                        candidate_text = None
                        if hasattr(alt_resp, "text") and alt_resp.text:
                            candidate_text = alt_resp.text
                        elif getattr(alt_resp, "candidates", None):
                            for c in alt_resp.candidates:
                                content = getattr(c, "content", None)
                                if content and getattr(content, "parts", None):
                                    for p in content.parts:
                                        pt = getattr(p, "text", None)
                                        if pt:
                                            candidate_text = pt
                                            break
                                    if candidate_text:
                                        break
                        if candidate_text:
                            if self._debug:
                                pass
                            self.resolved_model = alt
                            # Switch primary client to this working model for future calls
                            self._client = alt_client
                            self.model = alt
                            return candidate_text
                    except Exception:
                        if self._debug:
                            pass
                if self._debug:
                    pass
                # fall through to gemini if available
            if (self.backend == "vertex" or self.backend is None) and self._gemini_client:
                try:
                    gresp = self._gemini_client.models.generate_content(model=self.model, contents=prompt)
                    txt = getattr(gresp, "text", None)
                    if txt:
                        if self._debug:
                            pass
                        self.resolved_model = self.model
                        return txt
                except Exception:
                    if self._debug:
                        pass
                return None
            elif self.backend == "gemini":
                resp = self._client.models.generate_content(model=self.model, contents=prompt)
                txt = getattr(resp, "text", None)
                return txt
            else:
                return None
        except Exception:
            pass
            return None
