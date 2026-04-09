// Firebase Integration Helper
// Use isso para interagir com Firebase no seu app NexusLife

// Importar os serviços (eles já estão carregados via firebase-config.js)
import { auth, db, storage } from "./firebase-config.js";
import { 
    signInWithEmail, 
    signInWithGoogle, 
    signOut, 
    onAuthStateChanged 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

console.log("🔥 Firebase Helper carregado");

// Exemplo: Monitorar autenticação
onAuthStateChanged(auth, (user) => {
    if (user) {
        console.log("✅ Usuário autenticado:", user.email);
    } else {
        console.log("❌ Usuário não autenticado");
    }
});

// Exportar para uso em outros scripts
export { auth, db, storage };
