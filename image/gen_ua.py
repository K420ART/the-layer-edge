import random

class UserAgentGenerator:
    CHROME_VERSIONS = list(range(110, 127))
    FIREFOX_VERSIONS = list(range(90, 100))
    
    DEVICES = {
        "android": [
            "SM-G960F", "Pixel 5", "SM-A505F", "Pixel 4a", "OnePlus 9 Pro",
            "Xiaomi Mi 11", "Huawei P40", "Sony Xperia 1", "LG V60", "Nokia 9 PureView"
        ],
        "ios": ["iPhone 12", "iPhone 13", "iPhone 14", "iPhone SE"],
        "windows": ["10.0", "11.0"],
        "ubuntu": ["X86_64", "i686"]
    }
    
    ANDROID_VERSIONS = ["10.0", "11.0", "12.0", "13.0"]
    IOS_VERSIONS = ["13.0", "14.0", "15.0", "16.0"]
    
    def __init__(self, device_type='android', browser_type='chrome'):
        self.device_type = device_type
        self.browser_type = browser_type
    
    def _random_chrome_version(self):
        return f"{random.choice(self.CHROME_VERSIONS)}.{random.randint(0,9)}.{random.randint(1000,9999)}.{random.randint(0,99)}"
    
    def _random_firefox_version(self):
        return f"{random.choice(self.FIREFOX_VERSIONS)}.0"
    
    def generate(self):
        if self.browser_type == "chrome":
            browser_version = self._random_chrome_version()
        elif self.browser_type == "firefox":
            browser_version = self._random_firefox_version()
        else:
            return None

        if self.device_type == "android":
            return f"Mozilla/5.0 (Linux; Android {random.choice(self.ANDROID_VERSIONS)}; {random.choice(self.DEVICES['android'])}) " \
                   f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Mobile Safari/537.36"
        
        elif self.device_type == "ios":
            ios_version = random.choice(self.IOS_VERSIONS).replace(".", "_")
            return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) " \
                   f"AppleWebKit/537.36 (KHTML, like Gecko) CriOS/{browser_version} Mobile/15E148 Safari/604.1"
        
        elif self.device_type == "windows":
            return f"Mozilla/5.0 (Windows NT {random.choice(self.DEVICES['windows'])}; Win64; x64) " \
                   f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Safari/537.36"
        
        elif self.device_type == "ubuntu":
            return f"Mozilla/5.0 (X11; Ubuntu; Linux {random.choice(self.DEVICES['ubuntu'])}) " \
                   f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browser_version} Safari/537.36"
        
        return None
