# cybersecurity
cybersecurity pentesting tools and configuration

#!/bin/bash

LOG_DIR="/var/log/"
SUSPICIOUS_COMMANDS=("nc -l" "wget" "curl" "base64 -d" "chmod 777" "chown root" "rm -rf /" "dd if=")
SUSPICIOUS_FILES=("/root/.bash_history" "/var/log/auth.log" "/var/log/syslog" "/var/log/secure")

echo "🔍 **Loglarni tahlil qilinmoqda...**"
echo "-----------------------------------"

# **1. So'nggi 24 soat ichida o'zgargan fayllarni aniqlash**
echo "📂 **So'nggi 24 soat ichida o'zgargan log fayllar:**"
find "$LOG_DIR" -type f -mtime -1 -ls

echo "-----------------------------------"

# **2. Shubhali buyruqlarni aniqlash**
echo "⚠️ **Shubhali buyruqlar tekshirilmoqda...**"
for log in "${SUSPICIOUS_FILES[@]}"; do
    if [ -f "$log" ]; then
        for cmd in "${SUSPICIOUS_COMMANDS[@]}"; do
            grep -E "$cmd" "$log" &>/dev/null
            if [ $? -eq 0 ]; then
                echo "🚨 **$cmd** topildi faylda: $log"
                grep -E "$cmd" "$log"
                echo "-----------------------------------"
            fi
        done
    fi
done

# **3. SSH orqali noodatiy urinishlarni tekshirish**
echo "🔐 **SSH hujumlarini tekshirish...**"
grep "Failed password" /var/log/auth.log | tail -10
echo "-----------------------------------"

# **4. Root ruxsatlarini noqonuniy olishga urinishlar**
echo "🛑 **Root ruxsatlari tekshirilmoqda...**"
grep -E "sudo|su|root" /var/log/auth.log | tail -10
echo "-----------------------------------"

# **5. Foydalanuvchilar va noodatiy IP manzillarni tekshirish**
echo "🌍 **Tashqaridan kelgan ulanishlar tekshirilmoqda...**"
last | head -10
echo "-----------------------------------"

echo "✅ **Tekshiruv yakunlandi!**"



**XOTIRA QURILMALARI BILAN XAVFSIZ ISHLASH **
-	dd (Data Duplicator);
-	Autopsy;
-	Bulk Extractor va boshqalarwuni




