#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import uvicorn
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import wxmsg
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(
    "http://4e0146642a384204bb85061094a2f1ba@10.0.1.12:9000/2",
    traces_sample_rate=1.0
)

tags_metadata = [
    {
        "name": "WXAPI",
        "description": "Deploy **Jobs**."
    }
]

app = FastAPI(
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    title="CICD Tools",
    description="WeXin Deploy Jobs API",
    version="1.1"
)

origins = [
    "http://192.168.0.246:8000",
    "http://wecomapi.cuanon.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wxmsg.router)
app = SentryAsgiMiddleware(app)

if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app='main:app',
                host="0.0.0.0",
                port=8000,
                # reload=True,
                debug=True,
                proxy_headers=True,
                forwarded_allow_ips="10.0.1.5",
                log_config=log_config
                )
