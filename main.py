import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"), 
    base_url="https://api.siliconflow.cn/v1"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CopyRequest(BaseModel):
    product_info: str

@app.post("/api/generate")
async def generate_copy(req: CopyRequest):
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": "你是一个跨境电商文案专家。请根据商品信息，生成一段吸引人的英文产品描述，突出卖点，风格简洁有力。"},
            {"role": "user", "content": req.product_info}
        ],
        temperature=0.7,
    )
    return {"copy": response.choices[0].message.content}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)