{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import logging\
from opentelemetry import trace, metrics\
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter\
from opentelemetry.sdk.trace import TracerProvider\
from opentelemetry.sdk.trace.export import BatchSpanProcessor\
from prometheus_client import Counter, Histogram, start_http_server\
import time\
\
# Configure logging\
logging.basicConfig(level=logging.INFO)\
logger = logging.getLogger(__name__)\
\
# Configure tracing\
tracer_provider = TracerProvider()\
otlp_exporter = OTLPSpanExporter()\
span_processor = BatchSpanProcessor(otlp_exporter)\
tracer_provider.add_span_processor(span_processor)\
trace.set_tracer_provider(tracer_provider)\
tracer = trace.get_tracer(__name__)\
\
# Define metrics\
AI_REQUESTS = Counter(\
    'ai_requests_total',\
    'Total number of AI model requests',\
    ['model_name', 'status']\
)\
\
AI_LATENCY = Histogram(\
    'ai_request_latency_seconds',\
    'AI request latency in seconds',\
    ['model_name']\
)\
\
class AIObservability:\
    def __init__(self, service_name: str):\
        self.service_name = service_name\
        # Start Prometheus metrics server\
        start_http_server(8000)\
    \
    def track_request(self, func):\
        """Decorator to track AI model requests"""\
        def wrapper(*args, **kwargs):\
            model_name = kwargs.get('model_name', 'unknown')\
            \
            with tracer.start_as_current_span(\
                f"\{self.service_name\}_request"\
            ) as span:\
                span.set_attribute("model_name", model_name)\
                \
                start_time = time.time()\
                try:\
                    result = func(*args, **kwargs)\
                    AI_REQUESTS.labels(\
                        model_name=model_name,\
                        status="success"\
                    ).inc()\
                    return result\
                except Exception as e:\
                    AI_REQUESTS.labels(\
                        model_name=model_name,\
                        status="error"\
                    ).inc()\
                    span.set_attribute("error", str(e))\
                    logger.error(f"Error in AI request: \{e\}")\
                    raise\
                finally:\
                    duration = time.time() - start_time\
                    AI_LATENCY.labels(\
                        model_name=model_name\
                    ).observe(duration)\
        \
        return wrapper\
    \
    def log_model_performance(\
        self,\
        model_name: str,\
        input_tokens: int,\
        output_tokens: int,\
        duration: float\
    ):\
        """Log model performance metrics"""\
        logger.info(\
            f"Model: \{model_name\}, "\
            f"Input tokens: \{input_tokens\}, "\
            f"Output tokens: \{output_tokens\}, "\
            f"Duration: \{duration:.2f\}s"\
        )\
\
# Example usage\
if __name__ == "__main__":\
    observability = AIObservability("ai_service")\
    \
    @observability.track_request\
    def make_ai_request(text: str, model_name: str = "gpt-3.5-turbo"):\
        # Simulate AI request\
        time.sleep(0.5)\
        return "AI response"\
    \
    # Make sample request\
    try:\
        response = make_ai_request(\
            "Sample text",\
            model_name="gpt-3.5-turbo"\
        )\
    except Exception as e:\
        print(f"Error: \{e\}")}