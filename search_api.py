'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2025-06-09 14:57:09
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2025-06-09 15:10:48
FilePath: \class\search_api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import os
from dotenv import load_dotenv
import urllib.parse
import time

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="网页搜索 API",
    description="一个简单的网页搜索 API，支持网页内容抓取和搜索",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

@app.get("/")
async def root():
    return {"message": "欢迎使用网页搜索 API"}

@app.post("/search", response_model=List[SearchResult])
async def search(request: SearchRequest):
    try:
        # 使用百度搜索
        encoded_query = urllib.parse.quote(request.query)
        search_url = f"https://www.baidu.com/s?wd={encoded_query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        
        # 添加请求延迟，避免被封禁
        time.sleep(1)
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        
        # 解析百度搜索结果
        for result in soup.select('div.result.c-container')[:request.max_results]:
            title_element = result.select_one('h3.t')
            link_element = result.select_one('h3.t a')
            snippet_element = result.select_one('div.c-abstract')
            
            if title_element and link_element and snippet_element:
                search_results.append(SearchResult(
                    title=title_element.text.strip(),
                    url=link_element['href'],
                    snippet=snippet_element.text.strip()
                ))
        
        if not search_results:
            return []
            
        return search_results
    
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="搜索请求超时")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"搜索请求失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
