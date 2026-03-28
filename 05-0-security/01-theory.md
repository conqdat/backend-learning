# Phase 5: Spring Security & Authentication - Lý Thuyết

> **Thời gian:** 3 tuần
> **Mục tiêu:** Master Spring Security 6, OAuth2, JWT implementation

---

## 📚 BÀI 1: SPRING SECURITY CORE

### 1.1 Security Filter Chain

```
Request → Filter Chain → Controller → Response

Filter Chain (theo thứ tự):
1. SecurityContextPersistenceFilter
2. UsernamePasswordAuthenticationFilter
3. BasicAuthenticationFilter
4. RequestCacheAwareFilter
5. SecurityContextHolderAwareRequestFilter
6. AnonymousAuthenticationFilter
7. SessionManagementFilter
8. ExceptionTranslationFilter
9. FilterSecurityInterceptor
10. Your custom filters
```

### 1.2 Cấu hình Spring Security 6

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .addFilterBefore(jwtAuthenticationFilter(),
                UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

---

## 📚 BÀI 2: JWT AUTHENTICATION

### 2.1 JWT Token Structure

```
JWT = Header.Payload.Signature

Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user123",
  "name": "John Doe",
  "role": "USER",
  "iat": 1516239022,
  "exp": 1516242622
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

### 2.2 Access Token + Refresh Token Pattern

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ 1. Login (username, password)
       ▼
┌─────────────┐
│ Auth Server │─── 2. Validate credentials
└──────┬──────┘
       │ 3. Return:
       │    - Access Token (15 min)
       │    - Refresh Token (7 days)
       ▼
┌─────────────┐
│   Client    │─── 4. Call API với Access Token
└──────┬──────┘
       │
       │ 5. Access Token expired → 401
       ▼
┌─────────────┐
│   Client    │─── 6. Dùng Refresh Token request mới
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Auth Server │─── 7. Validate Refresh Token
└──────┬──────┘
       │ 8. Return new Access Token
       ▼
```

---

## 📚 BÀI 3: OAUTH2 RESOURCE SERVER

### 3.1 OAuth2 Roles

```
┌──────────────┐     ┌──────────────┐
│   Resource   │     │ Authorization│
│    Server    │     │    Server    │
│  (API backend)│     │  (Auth0, Okta)│
└──────────────┘     └──────────────┘
       │                    │
       │      Token         │
       │◄───────────────────│
       │                    │
       │   Request          │
       │◄───────────────────│
       │   with Token       │
       │                    │
       ▼                    ▼
┌────────────────────────────────┐
│            Client              │
│  (Web App, Mobile App, etc.)   │
└────────────────────────────────┘
```

### 3.2 Spring Security OAuth2 Resource Server

```java
@Configuration
@EnableWebSecurity
public class OAuth2Config {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt
                    .decoder(jwtDecoder())
                )
            );
        return http.build();
    }

    @Bean
    public JwtDecoder jwtDecoder() {
        String issuerUri = "https://your-auth-server.com";
        return NimbusJwtDecoder
            .withJwkSetUri(issuerUri + "/.well-known/jwks.json")
            .build();
    }
}
```

---

## 📝 TÓM TẮT PHASE 5

1. ✅ Spring Security filter chain
2. ✅ JWT token structure và validation
3. ✅ Access + Refresh token pattern
4. ✅ OAuth2 resource server configuration

---

## 🔜 TIẾP THEO

Phase 5 sẽ có examples và exercises thực tế!

---

## 📚 TÀI LIỆU THAM KHẢO

### Spring Security

| Resource | Link | Nội dung |
|----------|------|----------|
| Spring Security Reference | [Spring Docs](https://docs.spring.io/spring-security/reference/) | Official documentation |
| Spring Security 6 Migration | [Spring Guide](https://spring.io/blog/2022/02/21/spring-security-without-the-websecurityconfigureradapter) | Migrate to SecurityFilterChain |
| Baeldung Spring Security | [baeldung.com/spring-security](https://www.baeldung.com/security-spring) | Comprehensive tutorials |

### JWT Implementation

| Resource | Link | Nội dung |
|----------|------|----------|
| JWT.io | [jwt.io](https://jwt.io/) | JWT decoder/encoder, libraries |
| Introduction to JSON Web Tokens | [jwt.io/introduction](https://jwt.io/introduction/) | JWT basics |
| JWT Best Practices | [auth0.com](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/) | Security best practices |

### OAuth2 & OIDC

| Resource | Link | Nội dung |
|----------|------|----------|
| OAuth2 Simplified | [aaronparecki.com](https://aaronparecki.com/oauth-2-simplified/) | Easy to understand OAuth2 |
| OAuth2 Spec | [oauth.net/2](https://oauth.net/2/) | Official OAuth2 specification |
| OpenID Connect | [openid.net/connect](https://openid.net/connect/) | OIDC specification |

### Security Best Practices

| Resource | Link | Nội dung |
|----------|------|----------|
| OWASP Top 10 | [owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten/) | Most critical security risks |
| OWASP Cheat Sheet | [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/) | Security cheat sheets |
| Auth0 Blog | [auth0.com/blog](https://auth0.com/blog/) | Authentication & security articles |

### Password Storage

| Resource | Link | Nội dung |
|----------|------|----------|
| Password Storage Cheat Sheet | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | Secure password storage |
| BCrypt Explained | [windsock.io](https://windsock.io/what-exactly-is-bcrypt/) | Understanding bcrypt |
