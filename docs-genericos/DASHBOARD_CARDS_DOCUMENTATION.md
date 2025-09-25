# Componentes de Dashboard Card - Documentação

## Visão Geral

Este conjunto de componentes foi criado para padronizar os cards dos dashboards no projeto CRM-Ditual, seguindo as especificações de design e boas práticas estabelecidas.

## Componentes Disponíveis

### 1. StatsCard

Componente para exibir métricas principais com valores numéricos, tendências e ícones.

```tsx
import { StatsCard } from '../components/ui/DashboardCard';

<StatsCard
  title="Total de Orçamentos"
  value={150}
  prefix={<FileTextOutlined />}
  suffix=""
  color="#1890ff"
  trend={{ value: 12, isPositive: true }}
  description="vs mês anterior"
/>
```

**Props:**
- `title` (string): Título do card
- `value` (string | number): Valor principal a ser exibido
- `prefix?` (React.ReactNode): Ícone ou elemento antes do valor
- `suffix?` (string): Texto após o valor (ex: '%', 'R$')
- `color?` (string): Cor do tema (padrão: '#1890ff')
- `trend?` (object): Objeto com value (number) e isPositive (boolean)
- `description?` (string): Texto descritivo adicional
- `className?` (string): Classes CSS adicionais

**Especificações:**
- Altura fixa: 140px
- Layout responsivo
- Overflow de texto tratado
- Line-height mínimo: 1.4

### 2. StatusCard

Componente para indicadores de status com ícones e cores diferenciadas.

```tsx
import { StatusCard } from '../components/ui/DashboardCard';

<StatusCard
  title="Pendentes"
  value={25}
  icon={<ClockCircleOutlined />}
  color="#faad14"
  description="aguardando aprovação"
/>
```

**Props:**
- `title` (string): Título do card
- `value` (string | number): Valor do status
- `icon` (React.ReactNode): Ícone representativo
- `color` (string): Cor do tema
- `description?` (string): Texto descritivo adicional
- `className?` (string): Classes CSS adicionais

**Especificações:**
- Altura fixa: 120px
- Layout horizontal com ícone e conteúdo
- Fundo do ícone com transparência da cor principal

### 3. ProgressCard

Componente para mostrar progresso percentual com barras visuais.

```tsx
import { ProgressCard } from '../components/ui/DashboardCard';

<ProgressCard
  title="Meta Mensal de Vendas"
  progress={75.5}
  status="active"
  description="R$ 75.000 de R$ 100.000"
/>
```

**Props:**
- `title` (string): Título do card
- `progress` (number): Valor do progresso (0-100)
- `status?` ('active' | 'success' | 'exception' | 'normal'): Status do progresso
- `description?` (string): Texto descritivo adicional
- `className?` (string): Classes CSS adicionais

**Especificações:**
- Altura fixa: 180px
- Barra de progresso customizada
- Valores percentuais com 1 casa decimal
- Cores baseadas no status

### 4. InfoCard

Componente para exibir informações organizadas em grade.

```tsx
import { InfoCard } from '../components/ui/DashboardCard';

<InfoCard
  title="Informações do Perfil"
  items={[
    { label: 'Função', value: 'Administrador', color: '#1890ff' },
    { label: 'Status', value: 'Online', color: '#52c41a' },
    { label: 'Última Atividade', value: 'Agora', color: '#8c8c8c' },
    { label: 'ID', value: '#123', color: '#8c8c8c' }
  ]}
/>
```

**Props:**
- `title` (string): Título do card
- `items` (Array): Array de objetos com label, value e color opcional
- `className?` (string): Classes CSS adicionais

**Especificações:**
- Layout em grid 2x2 (responsivo para 1 coluna em mobile)
- Background diferenciado para itens (#fafafa)
- Altura mínima: 60px por item

### 5. BaseDashboardCard (DashboardCard)

Componente base para criação de cards customizados.

```tsx
import { DashboardCard } from '../components/ui/DashboardCard';

<DashboardCard height={200} hoverable={true}>
  {/* Conteúdo customizado */}
</DashboardCard>
```

**Props:**
- `children` (React.ReactNode): Conteúdo do card
- `className?` (string): Classes CSS adicionais
- `hoverable?` (boolean): Se deve ter efeito hover (padrão: true)
- `height?` (number | string): Altura do card

## Padrões de Design Seguidos

### 1. Alturas Consistentes
- **StatsCard**: 140px
- **StatusCard**: 120px  
- **ProgressCard**: 180px
- **InfoCard**: Altura automática baseada no conteúdo

### 2. Tratamento de Texto
- Line-height mínimo: 1.4
- Padding-bottom: 2px para evitar corte de baseline
- Overflow: hidden com text-overflow: ellipsis
- White-space: nowrap para valores importantes

### 3. Valores Percentuais
- Formato: XX.XX% (2 casas decimais para conversões)
- Formato: XX.X% (1 casa decimal para progressos)

### 4. Responsividade
- Grid responsivo: 4 colunas (desktop) → 2 colunas (tablet) → 1 coluna (mobile)
- Ajustes automáticos de altura em telas pequenas

### 5. Cores e Temas
- Primary: #1890ff (azul)
- Success: #52c41a (verde)
- Warning: #faad14 (amarelo)
- Error: #ff4d4f (vermelho)
- Secondary: #8c8c8c (cinza)

### 6. Efeitos de Interação
- Hover: box-shadow + translateY(-1px ou -2px)
- Transição suave: 0.3s ease
- Estados de loading com animação pulse

## Importação de Estilos

Sempre importe o arquivo CSS junto com os componentes:

```tsx
import '../styles/DashboardCard.css';
```

## Exemplo de Uso Completo

```tsx
import React from 'react';
import { Row, Col } from 'antd';
import { StatsCard, StatusCard, ProgressCard, InfoCard } from '../components/ui/DashboardCard';
import '../styles/DashboardCard.css';

const MyDashboard: React.FC = () => {
  return (
    <div style={{ padding: '24px' }}>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <StatsCard
            title="Vendas"
            value="R$ 125.430"
            prefix={<DollarOutlined />}
            color="#52c41a"
            trend={{ value: 15, isPositive: true }}
            description="este mês"
          />
        </Col>
        
        <Col xs={24} sm={12} lg={6}>
          <StatusCard
            title="Status"
            value="Ativo"
            icon={<CheckCircleOutlined />}
            color="#52c41a"
          />
        </Col>
        
        <Col xs={24} md={8}>
          <ProgressCard
            title="Meta Anual"
            progress={68.7}
            status="active"
            description="R$ 687.000 de R$ 1.000.000"
          />
        </Col>
        
        <Col xs={24} md={12}>
          <InfoCard
            title="Detalhes"
            items={[
              { label: 'Cliente', value: 'Empresa XYZ' },
              { label: 'Contrato', value: '#2024-001' }
            ]}
          />
        </Col>
      </Row>
    </div>
  );
};
```

## Manutenção e Extensibilidade

Os componentes foram desenvolvidos seguindo os princípios:

1. **Reutilização**: Componentes base que podem ser estendidos
2. **Consistência**: Padrões visuais unificados
3. **Acessibilidade**: Estrutura semântica e contraste adequado
4. **Performance**: Componentes leves e otimizados
5. **Manutenibilidade**: Código limpo e bem documentado

Para criar novos tipos de cards, estenda o `BaseDashboardCard` e siga os padrões estabelecidos nos componentes existentes.